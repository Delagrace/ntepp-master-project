const express = require('express');
const axios = require('axios');
const router = express.Router();
const FabricService = require('./fabricService');

const fabricService = new FabricService();
let addTempQueue = []; // Queue to store incoming addTemp transactions
let processingQueue = false; // Flag to indicate if the queue is being processed

// Server configuration
const currentServer = process.env.CURRENT_SERVER; // e.g., 'api3'
const nextServer = process.env.NEXT_SERVER; // e.g., 'http://api:3000'

// Middleware function to add timestamp to response
function addTimestamp(req, res, next) {
    // Add timestamp to response object
    res.timestamp = new Date().toISOString();
    next();
}

// Function to process addTemp transaction batches
async function processAddTempQueue() {
    if (processingQueue) return; // Avoid concurrent processing
    processingQueue = true;

    const delay = 300000 / 5000; // Milliseconds

    while (addTempQueue.length > 0) {
        const batch = addTempQueue.splice(0, 5000); // Get the next 60 addTemp transactions
        const batchPromises = batch.map(transaction => 
            fabricService.addTemp(transaction.username, transaction.channel, transaction.smartcontract, transaction.args)
        );

        await Promise.all(batchPromises);
        await new Promise(resolve => setTimeout(resolve, delay)); // Introduce delay between batches
    }

    // Notify the next server
    try {
        await axios.post(`${nextServer}/status`, { message: 'done' });
    } catch (error) {
        console.error(`Failed to notify the next server: ${error.message}`);
    }

    processingQueue = false;
}

// Middleware to process the queue at intervals
setInterval(() => {
    processAddTempQueue();
}, 60000); // Adjust the interval as needed

router.post("/enrollAdmin", addTimestamp, (req, res) => {
    fabricService.enrollAdmin(req.body.adminName, req.body.password).then((results) => {
        res.send({ timestamp: res.timestamp, result: results });
    });
});

router.post("/registerUser", addTimestamp, (req, res) => {
    fabricService.registerUser(req.body.adminName, req.body.username).then((results) => {
        res.send({ timestamp: res.timestamp, result: results });
    });
});

router.post("/registerSensor", addTimestamp, (req, res) => {
    console.log(req.body.args);
    fabricService.registerSensor(req.body.username, req.body.channel, req.body.smartcontract, req.body.args).then((results) => {
        res.send({ timestamp: res.timestamp, result: results });
    });
});

// Endpoint to receive addTemp transactions
router.post("/addTemp", addTimestamp, (req, res) => {
    const addTempTransaction = req.body; // Assuming the request body contains the entire addTemp transaction
    addTempQueue.push(addTempTransaction); // Add addTemp transaction to the queue
    res.send({ timestamp: res.timestamp, message: "addTemp transaction received and queued for processing" });
});

// Endpoint to receive status from the previous server
router.post("/status", (req, res) => {
    const { message } = req.body;
    if (message === 'done') {
        processAddTempQueue();
    }
    res.send({ message: 'Status received' });
});

router.post("/getHistory", addTimestamp, (req, res) => {
    fabricService.getHistory(req.body.username, req.body.channel, req.body.smartcontract, req.body.args).then((results) => {
        res.send({ timestamp: res.timestamp, result: results });
    });
});

module.exports = router;
