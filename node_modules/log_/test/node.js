'use strict';

var expect = require('expect.js');
var Log    = require('../index');

describe('log_', function () {

  var __log, log, message;

  before(function () {
    __log = console.log;
    console.log = function () {
      __log.apply(console, arguments);
      message = arguments;
    };
  });

  after(function () {
    console.log = __log;
  });

  it('should log', function () {
    log = Log('test', 'blue');
    log('hello', 'world');

    expect(message).to.have.length(3);
    expect(message[0]).to.equal('\u001b[34m[test]\u001b[0m');
    expect(message[1]).to.equal('hello');
    expect(message[2]).to.equal('world');
  });

  it('should warn', function () {
    log = Log('test', 'blue');
    log.warn('help!');

    expect(message).to.have.length(2);
    expect(message[0]).to.equal('\u001b[31m[test]\u001b[0m');
    expect(message[1]).to.equal('help!');
  });

});
