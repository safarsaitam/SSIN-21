const { execSync } = require('child_process');
const path = require('path');
const dotenv = require('dotenv');

dotenv.config();

const uri = `mongodb://${process.env.MONGO_HOSTNAME}:${process.env.MONGO_PORT}/${process.env.MONGO_DB}`;
const seeds = path.resolve('./database/seeds');
const commandWithPath = path.resolve('./node_modules/.bin/seed');

console.log( 'seed output -> ' + 
  execSync(
    `${commandWithPath} -u ${uri} --drop-database ${seeds}` //TODO add option --set-timestamps if feature added in next release
  )
);