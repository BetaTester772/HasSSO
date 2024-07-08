<script>
    import {onMount} from 'svelte';

    let redirectUrl = '';
    let onProgress = false;

    onMount(() => {
        const params = new URLSearchParams(window.location.search);
        redirectUrl = params.get('redirect')
        console.log(redirectUrl)
    });

    // http://localhost:5173/?redirect=http://localhost:5173/

    async function signIn(username, password, url) {
        console.log(url);
        onProgress = true;
        if (url === 'null') {
            url = window.location.origin;
        }
        try {
            const response = await fetch('https://ssoapi.betatester772.dev/api/v1/auth/verify', {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    intranet_id: username,
                    intranet_pw: password,
                    site_url: url

                })
            });

            const data = await response.json();

            if (response.ok) {
                const token = data.temp_token; // Assuming the token is in the 'token' field of the response
                // Save token to local storage or cookies if needed
                // localStorage.setItem('token', token);
                window.location.href = url + '?token=' + token;
            } else {
                console.error('Sign in failed with status:', response.status, response.statusText);
                alert(data.detail || 'An error occurred in the sign in process. Please try again later.');
            }
        } catch (error) {
            console.error('Sign in error:', error);
            alert('An error occurred. Please try again later.');
        } finally {
            onProgress = false;
        }
    }
</script>

<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your HaSSO
            account</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form class="space-y-6" action="#" method="POST"
              on:submit|preventDefault="{() => signIn(username.value, password.value, redirectUrl)}">
            <div>
                <label for="username" class="block text-sm font-medium leading-6 text-gray-900">Hana Intranet Id</label>
                <div class="mt-2">
                    <input id="username" name="username" type="text" autocomplete="username" required
                           class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-hana-600 sm:text-sm sm:leading-6">
                </div>
            </div>

            <div>
                <div class="flex items-center justify-between">
                    <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Hana Intranet
                        Password</label>
                    <div class="text-sm">
                        <a href="/update?redirect={redirectUrl}"
                           class="font-semibold text-hana-600 hover:text-hana-500">Password changed?</a>
                    </div>
                </div>
                <div class="mt-2">
                    <input id="password" name="password" type="password" autocomplete="current-password" required
                           class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-hana-600 sm:text-sm sm:leading-6">
                </div>
            </div>

            <div>
                <button type="submit" id="create-account"
                        class="flex w-full justify-center rounded-md px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm {onProgress ? 'bg-gray-400 cursor-not-allowed' : 'bg-hana-600 hover:bg-hana-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-hana-600'}"
                        disabled={onProgress}>
                    {#if onProgress}
                        Processing...
                    {/if}
                    {#if !onProgress}
                        Sign in
                    {/if}
                </button>

            </div>
        </form>

        <p class="mt-10 text-center text-sm text-gray-500">
            Not a member?
            <a href="/create?redirect={redirectUrl}"
               class="font-semibold leading-6 text-hana-600 hover:text-hana-500">Sign up</a>
        </p>
    </div>
</div>
