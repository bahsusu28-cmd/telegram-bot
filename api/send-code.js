const nodemailer = require('nodemailer');

// Email configuration
const transporter = nodemailer.createTransport({
    host: 'smtp.inbox.eu',
    port: 587,
    secure: false,
    auth: {
        user: 'verised@inbox.eu',
        pass: 'creator!!1340verised'
    }
});

// Store codes temporarily (in production use Redis or database)
const codes = new Map();

module.exports = async (req, res) => {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { email } = req.body;

    if (!email) {
        return res.status(400).json({ error: 'Email is required' });
    }

    // Generate 6-digit code
    const code = Math.floor(100000 + Math.random() * 900000).toString();

    // Store code with expiration (5 minutes)
    codes.set(email, {
        code: code,
        expires: Date.now() + 5 * 60 * 1000
    });

    try {
        // Send email
        await transporter.sendMail({
            from: '"Verised" <verised@inbox.eu>',
            to: email,
            subject: 'Код подтверждения Verised',
            html: `
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #ffc107;">⚡ Verised</h2>
                    <p>Ваш код подтверждения:</p>
                    <h1 style="color: #ffc107; font-size: 36px; letter-spacing: 5px;">${code}</h1>
                    <p style="color: #666;">Код действителен 5 минут.</p>
                    <p style="color: #999; font-size: 12px;">Если вы не запрашивали этот код, проигнорируйте это письмо.</p>
                </div>
            `
        });

        res.status(200).json({ success: true });
    } catch (error) {
        console.error('Email error:', error);
        res.status(500).json({ error: 'Failed to send email' });
    }
};

// Export codes for verification
module.exports.codes = codes;
