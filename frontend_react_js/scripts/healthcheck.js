#!/usr/bin/env node
/**
 * Simple healthcheck: verifies public/healthz.txt exists and prints OK.
 * This ensures container orchestrators probing /healthz can get a static OK via CRA static file serving.
 */
const fs = require('fs');
const path = require('path');

try {
  const healthPath = path.join(__dirname, '..', 'public', 'healthz.txt');
  if (fs.existsSync(healthPath)) {
    console.log('OK');
    process.exit(0);
  }
  console.error('healthz.txt not found');
  process.exit(1);
} catch (e) {
  console.error('Healthcheck error:', e.message);
  process.exit(1);
}
