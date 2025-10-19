// checkBrokenImports.js
const fs = require('fs');
const path = require('path');

const projectRoot = path.join(__dirname, 'src');

function fileExists(importPath, baseDir) {
  let fullPath = path.resolve(baseDir, importPath);

  // If no extension, check common ones
  if (!fs.existsSync(fullPath)) {
    const exts = ['.js', '.jsx', '.ts', '.tsx', '.json'];
    for (let ext of exts) {
      if (fs.existsSync(fullPath + ext)) return true;
    }
  } else {
    return true;
  }
  return false;
}

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
        const match = line.match(/import\s+.*?['"](.*?)['"]/);
        if (match) {
          const importPath = match[1];

          // Ignore package imports (react, axios, etc.)
          if (!importPath.startsWith('.') && !importPath.startsWith('/')) return;

          if (!fileExists(importPath, path.dirname(fullPath))) {
            console.log(`❌ Broken import in: ${fullPath}`);
            console.log(`   Line ${index + 1}: ${line}`);
            console.log('-------------------------');
          }
        }
      });
    }
  });
}

scanDir(projectRoot);
