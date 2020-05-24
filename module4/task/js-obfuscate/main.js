const code = `
let x = '1' + 1
console.log('x', x)
var $ = function(id) {
  return document.getElementById(id);
};
var a = 'hello world'
`

// js 混淆 初体验
const options = {
    compact: true,  // 代码压缩
    idenfierNamesGenerator: 'hexadecimal',  // 变量名替换
    idenfiersPrefix: 'germey', // 变量名前缀
    renaGlobals: true, // 混淆全局变量和函数名称
    // 混淆字符串
    stringArray: true,
    rotateStringArray: true,
    stringArrayEncoding: true, // 'base64' or 'rc4' or false
    stringArrayThreshold: 1,
    // unicode 转码
    unicodeEscapeSequence: true,
    // 代码自我保护 将混淆后的代码进行格式化（美化）或者重命名，该段代码将无法执行。
    selfDefending: true,
    // 控制流平坦 将代码的执行逻辑混淆，使其变得复杂难读。
    // 执行时间会变长，最长达 1.5 倍
    controlFlowFlattening: true,
    controlFlowFlatteningThreshold: 0.75,  // 控制比例
    // 僵尸代码注入
    deadCodeInjection: true,
    deadCodeInjectionThreshold: 0.4,  // 控制比例
    // 对象键名替换
    transformObjectKeys: true,
    // 禁用控制台输出
    disableConsoleOutput: true,
    // 调试保护 禁用调试模式
    debugProtection: true,
    // 域名锁定 代码只能在特定域名下运行
    domainLock: ['cuiqingcai.com']
}
const obfuscator = require('javascript-obfuscator')
function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}
console.log(obfuscate(code, options))

// 其他混淆和编码工具
// aaencode、jjencode、jsfuck 等工具

// js 加密技术  Emscripten 和 WebAssembly 等
// Emscripten 和 WebAssembly 等 能将 C/C++ 转成 JavaScript 引擎可以运行的代码。
// 可以将一些核心的功能利用 C/C++ 语言实现，形成浏览器字节码的形式。然后在 JavaScript 中调用
