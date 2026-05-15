'use strict'

const app = require('./app');
require('dotenv').config();

const PORT = process.env.PORT || 3000;

const server = app.listen(PORT, () => {
    console.log(`🚀 AI Agent Pro API Server started on port ${PORT}`);
});

process.on('SIGINT', () => {
    server.close(() => console.log('👋 API Server closed.'));
});
