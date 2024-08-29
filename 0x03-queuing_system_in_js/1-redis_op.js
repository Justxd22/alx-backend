import { createClient } from 'redis';

const redisClient = createClient();

redisClient.on('error', (error) => {
  console.log(`Redis client not connected to server: ${error.message}`);
  redisClient.quit();
});
redisClient.on('connect', () => console.log('Redis client connected to the server'));

const setNewSchool = function(schoolName, value){
    redisClient.set(schoolName, value, redis.print)
}

const displaySchoolValue = function(schoolName){
    redisClient.get(schoolName, (err, reply) => {
        if (err) {
            console.error(`Error getting value: ${err.message}`);
        } else {
            console.log(reply);
        }
    });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
