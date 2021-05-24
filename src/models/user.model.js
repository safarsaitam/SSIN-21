const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    username: {
        type: String,
        unique: true,
        required: true,
        maxLength: 8,
    },
    password: {
        type: String
    },
    full_name: {
        type: String,
        required: true,
    },
    security_level: {
        type: Number,
        required: true,
    },
    id: {
        type: String,
        default: '',
    },
    certificate: {
        type: String,
    },
    message_server_address: {
        type: String,
        default: '',
    },
    message_server_port: {
        type: Number,
    },
});

const User = mongoose.models.User
  ? mongoose.model('User')
  : mongoose.model('User', userSchema, 'users');
  
module.exports = User;