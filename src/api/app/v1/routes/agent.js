'use strict'

const express = require('express');
const agentController = require('../controllers/agent.controller');
const router = express.Router();

// Route: POST /api/v1/agent/query
router.post('/query', agentController.query);

// Route: POST /api/v1/agent/stream
router.post('/stream', agentController.stream);

module.exports = router;
