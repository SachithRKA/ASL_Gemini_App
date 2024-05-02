(function () {
  'use strict';

  var ansi = {
    'reset':      'colors: black',
    'bold':       'font-weight: bold',
    'italic':     'font-style: italic',
    'underline':  'text-decoration: underline',
    'black':      'color: #000',
    'red':        'color: red',
    'green':      'color: green',
    'yellow':     'color: yellow',
    'blue':       'color: blue',
    'magenta':    'color: magenta',
    'cyan':       'color: cyan',
    'white':      'color: white'
  };

  var enabled = true;

  var serialize = function (args) {
    var string = '';
    args.forEach(function (value) {
      string += ' ';
      if (typeof value === 'string') {
        string += value;
      } else {
        string += JSON.stringify(value, null, 4);
      }
    });
    return string;
  };

  var createLogger = function (name, color) {

    var prefix = '%c' + '[' + name + ']' + '%c';
    var style = color ? ansi[color] ? ansi[color] : color : '';

    var log = function () {
      if (! enabled) return;
      var args = __slice.call(arguments, 0);
      var contents = serialize(args);
      console.log(prefix + contents, style, ansi.reset);
    };

    log.warn = color === 'red' ? log : createLogger(name, 'red');

    return log;

  };

  createLogger.enable = function() {
    enabled = true;
  };

  createLogger.disable = function () {
    enabled = false;
  };

  createLogger.colors = ansi;

  if (typeof module !== 'undefined') {
    module.exports = createLogger;
  }

  this.Log = createLogger;

}).call(this);
