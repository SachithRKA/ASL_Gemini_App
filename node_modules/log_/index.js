var isNode = (typeof window === 'undefined');

if (isNode) {
  module.exports = require('./src/node');
} else {
  module.exports = require('./src/browser');
}
