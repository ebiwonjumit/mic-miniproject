'use strict';

var config = require('./config.webgme'),
    validateConfig = require('webgme/config/validator');

// Add/overwrite any additional settings here
// config.server.port = 8080;
// config.mongo.uri = 'mongodb://127.0.0.1:27018/mongoWEBGME';
config.mongo.uri = 'mongodb://mongo:27017/mongoWEBGME';


validateConfig(config);
module.exports = config;
