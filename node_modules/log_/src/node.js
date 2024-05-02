'use strict';

var ansi = {
  'reset':           0,

  'bold':            1,
  'italic':          3,
  'underline':       4,

  'black':           30,
  'red':             31,
  'green':           32,
  'yellow':          33,
  'blue':            34,
  'magenta':         35,
  'cyan':            36,
  'white':           37,

  'bright black':    90,
  'bright red':      91,
  'bright green':    92,
  'bright yellow':   93,
  'bright blue':     94,
  'bright magenta':  95,
  'bright cyan':     96,
  'bright white':    97,
};

for (var key in ansi) {
  if (! ansi.hasOwnProperty(key)) continue;
  ansi[key] = '\u001b[' + ansi[key] + 'm';
}

var enabled = true;

var createLogger = function (name, color) {
  var prefix, log;

  if (! color) color = 'reset';

  prefix = ansi[color] + '[' + name + ']' + ansi.reset;

  log = function () {
    if (! enabled) return;
    var args = Array.prototype.slice.call(arguments, 0);
    args.unshift(prefix);
    console.log.apply(console, args);
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

module.exports = createLogger;
