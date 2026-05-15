'use strict'

const express = require('express');
const agentController = require('../controllers/agent.controller');
const router = express.Router();

// Route: POST /api/v1/agent/query
router.post('/query', agentController.query);

module.exports = router;
