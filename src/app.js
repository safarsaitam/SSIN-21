const createError = require('http-errors');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const cors = require('cors');
const express = require('express');
const multer = require('multer');

let servicesRouter = require('./routes/services');
let authRouter = require('./routes/authentication');

const router = require('./routes/router');
require('dotenv').config();

const multerMid = multer({
  storage: multer.memoryStorage(),
});

// Our DB Configuration
require('./database/database');

// Seed DB
require('./database/seed');

// Create missing temporary user IDS
require('./database/create_user_ids');

const app = express();

app.use(cors());
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(multerMid.single('file'));

// Loads all the api routes
app.use('/services', servicesRouter);
app.use('/auth', authRouter);

// Optional fallthrough error handler
app.use((err, req, res) => {
  // The error id is attached to `res.sentry` to be returned
  // and optionally displayed to the user for support.
  res.statusCode = 500;
  // res.end(`${res.sentry}\n`);
});

// catch 404 and forward to error handler
app.use((req, res, next) => {
  next(createError(404));
});

// error handler
app.use((err, req, res) => {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  // res.render('error');
  res.json({ error: err });
});

module.exports = app;