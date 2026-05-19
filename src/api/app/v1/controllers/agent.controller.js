'use strict'

const AgentService = require('../services/agent.service');
const { OK } = require('../../../cores/success.response');

class AgentController {
    query = async (req, res, next) => {
        try {
            const result = await AgentService.queryWithRAG(req.body);
            new OK({
                message: 'Query successful',
                metadata: result
            }).send(res);
        } catch (error) {
            next(error);
        }
    }

    stream = async (req, res, next) => {
        try {
            const { stream, conversation_id } = await AgentService.streamWithRAG(req.body);

            res.setHeader('Content-Type', 'text/event-stream');
            res.setHeader('Cache-Control', 'no-cache');
            res.setHeader('Connection', 'keep-alive');

            let fullContent = '';
            let isFinished = false;

            const saveAndEnd = async () => {
                if (isFinished) return;
                isFinished = true;
                if (fullContent) {
                    try {
                        // Lưu vào DB ở chế độ background
                        AgentService.saveAIMessage(conversation_id, fullContent)
                            .catch(err => console.error('Background save error:', err));
                    } catch (err) {
                        console.error('Final save error:', err);
                    }
                }
                res.end();
            };

            stream.on('data', (chunk) => {
                const data = chunk.toString();
                res.write(data);

                const lines = data.split('\n');
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const content = line.replace('data: ', '');
                        if (content === '[DONE]') {
                            saveAndEnd();
                            return;
                        }
                        try {
                            const parsed = JSON.parse(content);
                            if (parsed.text) fullContent += parsed.text;
                        } catch (e) {}
                    }
                }
            });

            // Xử lý khi client đóng kết nối đột ngột
            req.on('close', () => {
                saveAndEnd();
            });

            stream.on('end', () => {
                saveAndEnd();
            });

            stream.on('error', (err) => {
                console.error('Stream error:', err);
                res.write(`data: ${JSON.stringify({ error: 'Stream error' })}\n\n`);
                saveAndEnd();
            });

        } catch (error) {
            next(error);
        }
    }
}

module.exports = new AgentController();
