<template>
  <nav id="sidebarMenu" class="sidebar d-md-block bg-dark text-light border-right border-light" style="max-width: 150px">
          <div class="sidebar">
            <ul class="nav flex-column ">
              <li class="nav-item">
                <router-link class="nav-link" to="/Dashboard">
                  Dashboard
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/Calendar">
                  Calendar
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/Status">
                  Status
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/Anime">
                  Anime
                </router-link>
              </li>
            </ul>

            <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
              <span>Settings</span>
            </h6>

            <ul class="nav flex-column mb-2 ">
              <li class="nav-item">
                <router-link class="nav-link" to="/Settings/Providers">
                  Providers
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/Settings/Anime">
                  Anime
                </router-link>
              </li>
            </ul>
            <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
              <span>Debug</span>
            </h6>
            <ul class="nav flex-column mb-2 ">
              <li class="nav-item">
                <router-link class="nav-link" to="/Debug/Graph">
                  Data Graph
                </router-link>
              </li>
            </ul>
          </div>
  </nav>
</template>

<style>
  .router-link-active,
  .router-link-exact-active {
   color: indianred;
   cursor: pointer;
 }
    sidebarMenu{
    /*height: 100%;*/
      position: absolute;
  }

</style>