'use strict'

const express = require('express');
const router = express.Router();

// V1 Routes
router.use('/v1/agent', require('./agent'));
router.use('/v1/analytics', require('./analytics'));

module.exports = router;
