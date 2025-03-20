const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');
const path = require('path')

// const FILE = 'table_1.pdf'
// const FILE = 'Year02.xls'
// const FILE = 'Year02.xls'
// const FILE = 'table.pdf'
// const FILE = 'table_p1.pdf'
// const FILE = 'table_p2_p3.pdf'
// const FILE = 'example.pdf'
// const FILE = '03.PNG'
// const FILE = 'red_dream.txt'
// const FILE = 'night.txt'
// const FILE = 'slide.pptx'
// const FILE = 'paper1.pdf'
const FILE = 'paprt2_table.pdf'

function removeResultMD() {
    const directory = __dirname; // 目前資料夾

    try {
        const files = fs.readdirSync(directory);

        files.forEach(file => {
            if (file.startsWith('result') && file.endsWith('.md')) {
                const filePath = path.join(directory, file);
                fs.unlinkSync(filePath);
                // console.log(`已刪除: ${file}`);
            }
        });

        console.log('所有符合條件的檔案已刪除完成。');
    } catch (err) {
        console.error('處理過程中發生錯誤:', err);
    }
}

async function uploadFile() {
    removeResultMD()
    try {
        // 構建 FormData
        const form = new FormData();
        form.append('file', fs.createReadStream(FILE));

        // 發送 POST 請求
        const response = await axios.post('http://localhost:8080/process', form, {
            headers: {
                ...form.getHeaders(),
            },
        });

        // 解析回應
        if (response.data && response.data.data && Array.isArray(response.data.data)) {
            response.data.data.forEach((item, index) => {
//                 console.log(item)
                const filename = `result${index + 1}.md`;
                fs.writeFileSync(filename, item, 'utf8');
                console.log(`Saved: ${filename}`, item.slice(0, 50));
            });
        } else {
            console.error('Unexpected response format:', response.data);
        }
    } catch (error) {
        console.error('Error:', error.message);
    }
}

uploadFile();
