<script>
    import {onMount} from 'svelte';

    let redirectUrl = '';

    onMount(() => {
        const params = new URLSearchParams(window.location.search);
        redirectUrl = params.get('redirect')
        console.log(redirectUrl)
    });

    // http://localhost:5173/?redirect=http://localhost:5173/

    async function signIn(username, password, url) {
        console.log(url);
        try {
            const response = await fetch('http://localhost:8000/api/v1/auth/verify', {
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
                        <a href="https://hi.hana.hs.kr/member/pop_idpw_search.asp" target="popup"
                           onclick="window.open('https://hi.hana.hs.kr/member/pop_idpw_search.asp','popup','width=600,height=600,scrollbars=no,resizable=no'); return false;"
                           class="font-semibold text-hana-600 hover:text-hana-500">Forgot password?</a>
                    </div>
                </div>
                <div class="mt-2">
                    <input id="password" name="password" type="password" autocomplete="current-password" required
                           class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-hana-600 sm:text-sm sm:leading-6">
                </div>
            </div>

            <div>
                <button type="submit"
                        class="flex w-full justify-center rounded-md bg-hana-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-hana-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-hana-600">
                    Sign in
                </button>
            </div>
        </form>

        <p class="mt-10 text-center text-sm text-gray-500">
            Not a member?
            <a href="https://hi.hana.hs.kr/member/step1.asp"
               class="font-semibold leading-6 text-hana-600 hover:text-hana-500">Sign up</a>
        </p>
    </div>
</div>
