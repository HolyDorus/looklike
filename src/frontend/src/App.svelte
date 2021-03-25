<script>
    import { Router, Route } from 'svelte-routing';

    import Index from './routes/Index.svelte';
    import Register from './routes/Register.svelte';
    import Login from './routes/Login.svelte';
    import Search from './routes/Search.svelte';
    import SearchResult from './routes/SearchResult.svelte';
    import Oops from './routes/Oops.svelte';
    import FavoriteCharacters from './routes/FavoriteCharacters.svelte';
    import NotFound404 from './routes/NotFound404.svelte';
</script>

<Router>
    <Route path='/' component={Index}/>
    <Route path='/register/' component={Register}/>
    <Route path='/login/' component={Login}/>
    <Route path='/search/' component={Search}/>
    <Route path='/search-result/' component={SearchResult}/>
    <Route path='/favorites/' component={FavoriteCharacters}/>

    <!-- Register Oops page -->
    <Route path='/oops/' component={Oops}/>

    <!-- Register 404 page route -->
    <Route component={NotFound404}/>
</Router>
