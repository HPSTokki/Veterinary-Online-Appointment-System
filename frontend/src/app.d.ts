// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		interface Locals {
			token: string | null
			user: {
				id: number,
				email: string,
				user_role: string,
				is_active: boolean
			} | null
		}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
