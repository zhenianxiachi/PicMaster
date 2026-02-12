import archiver from 'archiver';
import { createReadStream, readFileSync, readdirSync, statSync } from 'fs';
import { createWriteStream, existsSync, mkdirSync } from 'fs';
import { join, relative, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

/**
 * 获取当前日期时间字符串
 * @returns {string} 格式为 YYYYMMDD-HHMMSS
 */
function getTimestamp() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  return `${year}${month}${day}-${hours}${minutes}${seconds}`;
}

/**
 * 解析 .gitignore 文件
 * @param {string} gitignorePath .gitignore 文件路径
 * @returns {string[]} 排除规则列表
 */
function parseGitignore(gitignorePath) {
  if (!existsSync(gitignorePath)) {
    return [];
  }

  const content = readFileSync(gitignorePath, 'utf-8');
  const patterns = content
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith('#'));
  
  return patterns;
}

/**
 * 检查路径是否应该被排除
 * @param {string} relativePath 相对路径
 * @param {string[]} excludePatterns 排除模式列表
 * @returns {boolean} 是否应该排除
 */
function shouldExclude(relativePath, excludePatterns) {
  // 额外排除 .git 目录
  if (relativePath.startsWith('.git')) {
    return true;
  }

  for (const pattern of excludePatterns) {
    let regex;
    if (pattern.startsWith('!')) {
      continue; // 忽略否定规则
    }

    if (pattern.includes('*')) {
      // 转换 glob 模式为正则表达式
      regex = new RegExp(
        '^' +
          pattern
            .replace(/\./g, '\\.')
            .replace(/\*/g, '.*')
            .replace(/\?/g, '.') +
          '$'
      );
    } else if (pattern.endsWith('/')) {
      // 目录
      regex = new RegExp('^' + pattern.replace(/\//g, '\\/') + '.*');
    } else {
      // 文件或目录
      regex = new RegExp(
        '^' +
          pattern.replace(/\./g, '\\.').replace(/\//g, '\\/') +
          '(\\/.*|$)'
      );
    }

    if (regex.test(relativePath)) {
      return true;
    }
  }

  return false;
}

/**
 * 递归获取目录下的所有文件
 * @param {string} dirPath 目录路径
 * @param {string} baseDir 基础目录路径
 * @param {string[]} excludePatterns 排除模式列表
 * @returns {string[]} 文件路径列表
 */
function getFiles(dirPath, baseDir, excludePatterns) {
  const files = [];
  const items = readdirSync(dirPath);

  for (const item of items) {
    const fullPath = join(dirPath, item);
    const relativePath = relative(baseDir, fullPath);

    if (shouldExclude(relativePath, excludePatterns)) {
      continue;
    }

    const stat = statSync(fullPath);
    if (stat.isDirectory()) {
      files.push(...getFiles(fullPath, baseDir, excludePatterns));
    } else if (stat.isFile()) {
      files.push(fullPath);
    }
  }

  return files;
}

/**
 * 打包源代码为 ZIP 文件
 */
async function packageSource() {
  const projectRoot = join(__dirname, '..');
  const gitignorePath = join(projectRoot, '.gitignore');
  const outputDir = join(projectRoot, 'release');
  const timestamp = getTimestamp();
  const zipFileName = `picmaster-frontend-${timestamp}.zip`;
  const zipFilePath = join(outputDir, zipFileName);

  console.log('📦 开始打包源代码...');

  // 确保输出目录存在
  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }

  // 解析 .gitignore
  const excludePatterns = parseGitignore(gitignorePath);
  console.log(`📋 排除规则: ${excludePatterns.length} 条`);

  // 获取所有文件
  const files = getFiles(projectRoot, projectRoot, excludePatterns);
  console.log(`📄 找到文件: ${files.length} 个`);

  // 创建 ZIP 文件
  const output = createWriteStream(zipFilePath);
  const archive = archiver('zip', {
    zlib: { level: 9 }, // 最高压缩级别
  });

  return new Promise((resolve, reject) => {
    output.on('close', () => {
      const fileSizeInMB = (archive.pointer() / 1024 / 1024).toFixed(2);
      console.log(`✅ 打包完成!`);
      console.log(`📁 文件位置: ${zipFilePath}`);
      console.log(`📊 文件大小: ${fileSizeInMB} MB`);
      resolve();
    });

    archive.on('error', (err) => {
      console.error('❌ 打包失败:', err);
      reject(err);
    });

    archive.pipe(output);

    // 添加文件到 ZIP
    for (const file of files) {
      const relativePath = relative(projectRoot, file);
      archive.file(file, { name: relativePath });
    }

    // 完成打包
    archive.finalize();
  });
}

// 执行打包
packageSource().catch(console.error);
