import CryptoJS from 'crypto-js'
import _crypto from '@/config/key'

const { key, iv } = _crypto
const encryptKey = CryptoJS.enc.Utf8.parse(key)
const encryptIv = CryptoJS.enc.Utf8.parse(iv)

function dataDecrypt(word) {
    let decrypt = CryptoJS.AES.decrypt(word, encryptKey, { iv: encryptIv , mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 });
    let decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
    return decryptedStr.toString();
}

/**AES加密数据（注：无需提前将其转为string，如果类型传入object的对象可以自动将其stringify再加密） */
function dataEncrypt(word) {
    let data = typeof word == 'object' ? JSON.stringify(word) : word
    let srcs = CryptoJS.enc.Utf8.parse(data);
    let encrypted = CryptoJS.AES.encrypt(srcs, encryptKey, { iv: encryptIv , mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 });
    return encrypted.toString();
}

export {dataDecrypt, dataEncrypt}