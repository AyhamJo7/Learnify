import express from 'express';
import dotenv from 'dotenv';
import authRoutes from './routes/authRoutes';
import { verifyJWT } from './middlewares/authMiddleware';
import db from './database/db';

dotenv.config();

const app = express();
const port = process.env.PORT || 5000;

// Middleware
app.use(express.json());
app.use('/api/auth', authRoutes);

// Protected route example
app.get('/api/protected', verifyJWT, (req, res) => {
  res.json({ message: 'This is a protected route.' });
});

// Start server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});