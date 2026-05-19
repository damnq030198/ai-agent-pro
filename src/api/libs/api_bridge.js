'use strict'

const axios = require('axios');

class APIBridge {
    static async callPython(query, model_id = null) {
        const inferenceUrl = process.env.INFERENCE_URL || 'http://localhost:8000';
        try {
            const response = await axios.post(`${inferenceUrl}/generate`, {
                query,
                model_id: model_id || 'gemini-1.5-pro'
            });
            return response.data;
        } catch (error) {
            console.error(`DEBUG: APIBridge error: ${error.message}`);
            throw new Error('Failed to connect to AI Inference Engine');
        }
    }

    /**
     * Get a readable stream from the Python Inference Server
     */
    static async streamPython(query, model_id = null) {
        const inferenceUrl = process.env.INFERENCE_URL || 'http://localhost:8000';
        try {
            const response = await axios({
                method: 'post',
                url: `${inferenceUrl}/stream`,
                data: {
                    query,
                    model_id: model_id || 'gemini-1.5-pro'
                },
                responseType: 'stream'
            });
            return response.data;
        } catch (error) {
            console.error(`DEBUG: APIBridge streaming error: ${error.message}`);
            throw new Error('Failed to connect to AI Inference Engine (Streaming)');
        }
    }
}

module.exports = APIBridge;
