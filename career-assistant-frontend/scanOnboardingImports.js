// scanOnboardingImports.js
const fs = require('fs');
const path = require('path');

const projectRoot = path.join(__dirname, 'src');

function scanDir(dir) {
  const files = fs.readdirSync(dir);
  files.forEach(file => {
    const fullPath = path.join(dir, file);
    const stats = fs.statSync(fullPath);

    if (stats.isDirectory()) {
      scanDir(fullPath);
    } else if (file.endsWith('.js') || file.endsWith('.jsx')) {
      const content = fs.readFileSync(fullPath, 'utf-8');
      const lines = content.split('\n');
      lines.forEach((line, index) => {
        if (/onboarding\s*form/i.test(line)) {
          console.log(`File: ${fullPath}`);
          console.log(`Line ${index + 1}: ${line}`);
          console.log('-------------------------');
        }
      });
    }
  });
}

scanDir(projectRoot);
