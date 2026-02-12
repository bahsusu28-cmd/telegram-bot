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
        // Using Gmail SMTP
        const transporter = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: 'verised.noreply@gmail.com',
                pass: 'xqjp yzmt hqwk zrxb' // App password
            }
        });

        await transporter.sendMail({
            from: '"Verised" <verised.noreply@gmail.com>',
            to: email,
            subject: 'Verised - Код подтверждения',
            text: `Ваш код подтверждения: ${code}\n\nКод действителен 5 минут.\n\nЕсли вы не запрашивали этот код, проигнорируйте письмо.`,
            html: `
                <div style="background:#000;color:#fff;padding:40px;font-family:Arial,sans-serif;text-align:center;max-width:600px;margin:0 auto;">
                    <h1 style="color:#fff;font-size:28px;margin-bottom:20px;">⚡ Verised</h1>
                    <p style="font-size:16px;color:#999;margin-bottom:30px;">Ваш код подтверждения:</p>
                    <div style="background:#1a1a1a;padding:20px;border-radius:12px;margin:20px 0;">
                        <h2 style="color:#fff;font-size:48px;letter-spacing:8px;margin:0;">${code}</h2>
                    </div>
                    <p style="font-size:14px;color:#666;margin-top:30px;">Код действителен 5 минут</p>
                    <p style="font-size:12px;color:#444;margin-top:20px;">Если вы не запрашивали этот код, проигнорируйте письмо</p>
                </div>
            `
        });

        console.log('✅ Email sent to:', email);
        console.log('🔑 Code:', code);
        
        return res.status(200).json({ 
            success: true,
            code: code // For testing
        });
    } catch (error) {
        console.error('❌ Email Error:', error.message);
        console.log('🔑 Code saved for', email, ':', code);
        
        return res.status(200).json({ 
            success: true,
            code: code
        });
    }
}
