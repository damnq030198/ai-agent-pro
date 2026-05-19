'use strict'

const APIBridge = require('../../../libs/api_bridge');
const prisma = require('../../../dbs/init.postgresql');

class AgentService {
    static async queryWithRAG({ query, model_id, conversation_id = null }) {
        // ... (giữ nguyên code cũ để tương thích ngược)
        try {
            let conversation = conversation_id ? await prisma.conversation.findUnique({ where: { id: conversation_id } }) : null;
            if (!conversation) conversation = await prisma.conversation.create({ data: { title: query.substring(0, 30) } });
            
            await prisma.message.create({ data: { role: 'user', content: query, conversationId: conversation.id } });
            const result = await APIBridge.callPython(query, model_id);
            await prisma.message.create({ data: { role: 'ai', content: result.response || result, conversationId: conversation.id } });

            return { ...result, conversation_id: conversation.id };
        } catch (error) {
            console.error(`DEBUG: Error in queryWithRAG: ${error.stack || error}`);
            throw error;
        }
    }

    static async streamWithRAG({ query, model_id, conversation_id = null }) {
        try {
            // 1. Lấy hoặc tạo Conversation
            let conversation = conversation_id ? await prisma.conversation.findUnique({ where: { id: conversation_id } }) : null;
            if (!conversation) {
                conversation = await prisma.conversation.create({ data: { title: query.substring(0, 30) } });
            }

            // 2. Lưu tin nhắn User
            await prisma.message.create({
                data: {
                    role: 'user',
                    content: query,
                    conversationId: conversation.id
                }
            });

            // 3. Lấy stream từ Python Engine
            const stream = await APIBridge.streamPython(query, model_id);

            return {
                stream,
                conversation_id: conversation.id
            };
        } catch (error) {
            console.error(`DEBUG: Error in streamWithRAG: ${error.stack || error}`);
            throw error;
        }
    }

    static async saveAIMessage(conversation_id, content) {
        return await prisma.message.create({
            data: {
                role: 'ai',
                content,
                conversationId: conversation_id
            }
        });
    }
}

module.exports = AgentService;
