<script>
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';

    import Header from '../components/Header.svelte';

    import { logOut } from '../auth.js'


    onMount(() => {
        logOut();
        navigate('/');
    });
</script>

<Header/>
