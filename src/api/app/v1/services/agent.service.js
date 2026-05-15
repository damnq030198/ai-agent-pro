'use strict'

const APIBridge = require('../../libs/api_bridge');
const prisma = require('../../../dbs/init.postgresql');

class AgentService {
    static async queryWithRAG({ query, model_id, conversation_id = null }) {
        // 1. Tạo hoặc lấy Conversation
        let conversation;
        if (conversation_id) {
            conversation = await prisma.conversation.findUnique({ where: { id: conversation_id } });
        }
        
        if (!conversation) {
            conversation = await prisma.conversation.create({ data: { title: query.substring(0, 30) } });
        }

        // 2. Lưu tin nhắn User vào Postgres
        await prisma.message.create({
            data: {
                role: 'user',
                content: query,
                conversationId: conversation.id
            }
        });

        // 3. Lấy 5 tin nhắn gần nhất để làm ngữ cảnh (Memory)
        const history = await prisma.message.findMany({
            where: { conversationId: conversation.id },
            orderBy: { timestamp: 'asc' },
            take: 10
        });

        // 4. Gọi sang AI Engine (có gửi kèm history)
        const result = await APIBridge.callPython(query, model_id, history);

        // 5. Lưu tin nhắn AI vào Postgres
        await prisma.message.create({
            data: {
                role: 'ai',
                content: result.response || result,
                conversationId: conversation.id
            }
        });

        return {
            ...result,
            conversation_id: conversation.id
        };
    }
}

module.exports = AgentService;
