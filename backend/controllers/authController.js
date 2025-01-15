import { getUserByEmail, createUser } from '../models/User';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

export const login = async (req, res) => {
  const { email, password } = req.body;
  const user = await getUserByEmail(email);
  if (!user) return res.status(400).json({ message: 'User not found.' });

  const passwordMatch = await bcrypt.compare(password, user.password);
  if (!passwordMatch) return res.status(400).json({ message: 'Invalid credentials.' });

  const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET);
  res.json({ token });
};

export const register = async (req, res) => {
  const { email, password } = req.body;
  const existingUser = await getUserByEmail(email);
  if (existingUser) return res.status(400).json({ message: 'Email already in use.' });

  const hashedPassword = await bcrypt.hash(password, 10);
  const user = await createUser(email, hashedPassword);
  res.status(201).json({ message: 'User created successfully.' });
};