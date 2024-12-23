import Vue from "vue";
import Router from "vue-router";

import LoginPage from "./components/LoginPage.vue";
import HomePage from "./components/HomePage.vue";
import SignUp from "./components/SignUp.vue";
import AdminDashboard from "./components/AdminDashboard.vue";
import AdminLogin from "./components/AdminLogin.vue";
import AdminUsers from "./components/AdminComponents/AdminUsers.vue";
import AdminService from "./components/AdminComponents/AdminService.vue";
import AdminVerification from "./components/AdminComponents/AdminVerification.vue";
import UserDashboard from "./components/UserComponents/UserDashboard.vue";
import SearchResults from "./components/UserComponents/SearchResults.vue";
import UserServices from "./components/UserComponents/UserServices.vue";
import UserCard from "./components/UserComponents/UserCard.vue";
import AdminStats from '@/components/AdminComponents/AdminStats.vue'
import AdminServiceRequest from "./components/AdminComponents/AdminServiceRequest.vue";
import AboutUs from "./components/AboutUs.vue";


Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "Home",
      component: HomePage,
    },
    {
      path: "/about-us",
      name: "AboutUs",
      component : AboutUs,
    },
    {
      path: "/login",
      name: "LoginPage",
      component: LoginPage,
    },
    {
      path: "/sign-up",
      name: "SignUp",
      component: SignUp,
    },
    {
      path: "/user",
      component: UserDashboard,
      children: [
        {
          path: "",  // This makes it the default route
          name: "UserDashboard",
          component: UserCard
        },
        {
          path: "search",
          name: "SearchResults",
          component: SearchResults
        },
        {
          path: "user-services",
          name: "UserServices",
          component: UserServices
        },
      ]
    },
    {
      path: "/admin",
      name: "AdminDashboard",
      component: AdminDashboard,
      redirect: { name: 'admin-stats' },
      children: [
        {
          path: "", // Empty path
          name: 'admin-stats',
          component: AdminStats
        },
        {
          path: "users",
          name: "admin-users",
          component: AdminUsers,
        },
        {
          path: "services",
          name: "admin-services",
          component: AdminService,
        },
        {
          path: "verifyProfessional",
          name: "admin-verification",
          component: AdminVerification,
        },
        {
          path : "adminServiceRequests",
          name: "admin-sr",
          component: AdminServiceRequest
        }
      ],
    },
    {
      path: "/admin-login",
      name: "AdminLogin",
      component: AdminLogin,
    },

  ],
});
