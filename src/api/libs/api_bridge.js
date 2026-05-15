'use strict'

const { exec } = require('child_process');
const path = require('path');

class APIBridge {
    static async callPython(query, model_id = null) {
        return new Promise((resolve, reject) => {
            const pythonScript = path.join(__dirname, '../../../scripts/api_bridge.py');
            const command = `python "${pythonScript}" --query "${query}" ${model_id ? `--model ${model_id}` : ''}`;

            exec(command, (error, stdout, stderr) => {
                if (error) {
                    return reject({
                        message: 'Error calling AI Engine',
                        details: stderr
                    });
                }
                
                try {
                    const response = JSON.parse(stdout);
                    resolve(response);
                } catch (e) {
                    resolve({ response: stdout.trim() });
                }
            });
        });
    }
}

module.exports = APIBridge;
