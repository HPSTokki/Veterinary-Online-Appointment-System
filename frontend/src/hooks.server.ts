import type { Handle } from "@sveltejs/kit";

const API_URL = process.env.API_URL ?? 'http://localhost:8000'
const CHAIN_URL = `https://veterinary-online-appointment-syste.vercel.app/${API_URL}`

export const handle: Handle = async ({ event, resolve }) => {
    const token = event.cookies.get('token')
    if (token) {
        try {
            const response = await fetch(`${CHAIN_URL}/user/me`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            if (response.ok) {
                const user = await response.json()
                event.locals.user = user
                event.locals.token = token
                console.log('locals.user:', event.locals.user)
            }
        } catch (error) {
            console.log(error)
        }
    }
    return resolve(event)
}