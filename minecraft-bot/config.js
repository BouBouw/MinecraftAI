/**
 * Bot configuration
 */
export const config = {
    // Server connection
    server: {
        host: process.env.MC_HOST || 'localhost',
        port: parseInt(process.env.MC_PORT) || 25565,
        username: process.env.MC_USERNAME || 'AI_Builder',
        password: process.env.MC_PASSWORD || null,
        auth: process.env.MC_AUTH || 'microsoft' // 'microsoft' or 'offline'
    },

    // Bot behavior
    startFromScratch: true,
    initialEquipment: [],

    // AI/ML settings
    rlModel: './models/best_model.zip',
    useRL: false, // Set to true after training
    learningRate: 0.001,

    // Communication
    coordinatorUrl: 'ws://localhost:8080/bot',

    // Building settings
    buildSpeed: 'normal', // 'slow', 'normal', 'fast'
    maxReachDistance: 4.5, // blocks

    // Resource gathering
    autoGatherResources: true,
    miningDepth: 60, // Y level
    preferSurfaceResources: true,

    // Pathfinding
    pathfindingTimeout: 10000, // ms
    avoidMobs: true,

    // Logging
    logLevel: 'info' // 'debug', 'info', 'warn', 'error'
};
