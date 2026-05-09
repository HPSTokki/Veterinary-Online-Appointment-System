import { fail } from '@sveltejs/kit';
import type { Actions } from './$types';
import { forgotPassword, resetPassword } from '$lib/api/auth';

export const actions: Actions = {
	request_pin: async ({ request }) => {
		const form = await request.formData();
		const email = form.get('email') as string;

		try {
			await forgotPassword(email);
			// Backend always returns success regardless of whether email exists (security)
			return { pin_sent: true, email };
		} catch (error: any) {
			return fail(400, { message: error.message || 'Failed to send PIN. Please try again.' });
		}
	},

	reset_password: async ({ request }) => {
		const form = await request.formData();
		const email = form.get('email') as string;
		const pin = form.get('pin') as string;
		const new_password = form.get('new_password') as string;

		try {
			await resetPassword({ email, pin, new_password });
			return { reset_success: true };
		} catch (error: any) {
			return fail(400, { message: error.message || 'Invalid or expired PIN.' });
		}
	}
};
