const express = require('express');
const { createClient } = require('redis');
const { promisify } = require('util');
const kue = require('kue');

// Create Redis client
const client = createClient();
client.on('error', (err) => console.error('Redis Client Error:', err));
client.connect();

// Promisify Redis client methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Initialize variables
const app = express();
const port = 1245;
const queue = kue.createQueue();
let reservationEnabled = true;

// Functions to reserve and get available seats
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return parseInt(seats, 10);
}

// Initialize available seats to 50
(async () => {
  await reserveSeat(50);
})();

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
      return;
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  }).on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

// Route to process the queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats();

    if (currentSeats <= 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
      return;
    }

    const newSeats = currentSeats - 1;
    await reserveSeat(newSeats);

    if (newSeats === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
