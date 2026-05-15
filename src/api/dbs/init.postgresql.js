'use strict'

const { PrismaClient } = require('@prisma/client');

class PrismaDatabase {
    constructor() {
        this.prisma = new PrismaClient();
    }

    async connect() {
        try {
            await this.prisma.$connect();
            console.log('🐘 PostgreSQL connected successfully via Prisma');
        } catch (error) {
            console.error('❌ PostgreSQL connection error:', error);
        }
    }
}

const dbInstance = new PrismaDatabase();
module.exports = dbInstance.prisma;
