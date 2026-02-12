const nodemailer = require('nodemailer');

global.codes = global.codes || new Map();

export default async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { email } = req.body;

    if (!email) {
        return res.status(400).json({ error: 'Email is required' });
    }

    const code = Math.floor(100000 + Math.random() * 900000).toString();

    global.codes.set(email, {
        code: code,
        expires: Date.now() + 5 * 60 * 1000
    });

    try {
        const transporter = nodemailer.createTransport({
            host: 'smtp.inbox.eu',
            port: 587,
            secure: false,
            auth: {
                user: 'verised@inbox.eu',
                pass: 'creator!!1340verised'
            },
            tls: {
                ciphers: 'SSLv3',
                rejectUnauthorized: false
            }
        });

        const info = await transporter.sendMail({
            from: 'verised@inbox.eu',
            to: email,
            subject: 'Verised - Код подтверждения',
            text: `Ваш код: ${code}`,
            html: `
                <div style="background:#000;color:#fff;padding:40px;font-family:Arial,sans-serif;text-align:center;">
                    <h1 style="color:#fff;font-size:28px;margin-bottom:20px;">⚡ Verised</h1>
                    <p style="font-size:16px;color:#999;margin-bottom:30px;">Ваш код подтверждения:</p>
                    <div style="background:#1a1a1a;padding:20px;border-radius:12px;margin:20px 0;">
                        <h2 style="color:#fff;font-size:48px;letter-spacing:8px;margin:0;">${code}</h2>
                    </div>
                    <p style="font-size:14px;color:#666;margin-top:30px;">Код действителен 5 минут</p>
                </div>
            `
        });

        console.log('✅ Email sent:', info.messageId);
        return res.status(200).json({ success: true });
    } catch (error) {
        console.error('❌ SMTP Error:', error);
        
        // Return success anyway so user can enter code
        return res.status(200).json({ 
            success: true,
            warning: 'Email may not be delivered',
            testCode: code
        });
    }
}
