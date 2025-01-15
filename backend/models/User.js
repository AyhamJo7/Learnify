import { query } from '../database/db';

export const getUserByEmail = async (email) => {
  const { rows } = await query('SELECT * FROM users WHERE email = $1', [email]);
  return rows[0];
};

export const createUser = async (email, password) => {
  const { rows } = await query(
    'INSERT INTO users (email, password) VALUES ($1, $2) RETURNING *',
    [email, password]
  );
  return rows[0];
};