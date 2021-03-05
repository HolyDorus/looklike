<script>
    import { Router, Route } from 'svelte-routing';

    import Index from './routes/Index.svelte';
    import Search from './routes/Search.svelte';
    import SearchResult from './routes/SearchResult.svelte';
    import Oops from './routes/Oops.svelte';
    import NotFound404 from './routes/NotFound404.svelte';
</script>

<Router>
    <Route path='/' component={Index}/>
    <Route path='/search/' component={Search}/>
    <Route path='/search-result/' component={SearchResult}/>

    <!-- Register Oops page -->
    <Route path='/oops/' component={Oops}/>

    <!-- Register 404 page route -->
    <Route component={NotFound404}/>
</Router>
