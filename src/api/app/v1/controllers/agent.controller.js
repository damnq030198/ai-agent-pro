'use strict'

const AgentService = require('../services/agent.service');
const { OK } = require('../../../cores/success.response');

class AgentController {
    query = async (req, res, next) => {
        new OK({
            message: 'Query successful',
            metadata: await AgentService.queryWithRAG(req.body)
        }).send(res);
    }
}

module.exports = new AgentController();
