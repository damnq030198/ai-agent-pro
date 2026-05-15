'use strict'

const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');
const { OK } = require('../../../cores/success.response');

router.get('/usage', async (req, res, next) => {
    const logPath = path.join(__dirname, '../../../../data/logs/token_usage.jsonl');
    
    let totalInput = 0;
    let totalOutput = 0;
    let history = [];

    if (fs.existsSync(logPath)) {
        const lines = fs.readFileSync(logPath, 'utf-8').split('\n').filter(Boolean);
        history = lines.map(line => {
            const data = JSON.parse(line);
            totalInput += data.usage.input_tokens;
            totalOutput += data.usage.output_tokens;
            return data;
        });
    }

    // Ước tính chi phí (giá giả định)
    const estimatedCost = (totalInput * 0.003 / 1000) + (totalOutput * 0.015 / 1000);

    new OK({
        message: 'Usage analytics retrieved',
        metadata: {
            total_input_tokens: totalInput,
            total_output_tokens: totalOutput,
            estimated_cost_usd: estimatedCost.toFixed(4),
            request_count: history.length,
            history: history.slice(-10) // Trả về 10 giao dịch gần nhất
        }
    }).send(res);
});

module.exports = router;
