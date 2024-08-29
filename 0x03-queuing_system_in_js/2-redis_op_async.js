import { createClient } from 'redis';
import { promisify } from 'util';

const redisClient = createClient();

redisClient.on('error', (error) => {
  console.log(`Redis client not connected to server: ${error.message}`);
  redisClient.quit();
});
redisClient.on('connect', () => console.log('Redis client connected to the server'));

const getAsync = promisify(redisClient.get).bind(redisClient);

const setNewSchool = function(schoolName, value){
    redisClient.set(schoolName, value, redis.print)
}

async function displaySchoolValue(schoolName){
    const value = await getAsync(schoolName);
    if (value) console.log(value);
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
