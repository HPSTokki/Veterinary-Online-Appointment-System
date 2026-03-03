<script>
    import VetLogo from '$lib/assets/VetLogo.png'
</script>

<div class="navbar bg-main shadow-sm">
    <div class="navbar-start">
        <div class="dropdown">
            <div tabindex="0" role="button" class="btn btn-ghost hover:bg-sub hover:border-sub lg:hidden">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" /> </svg>
            </div>
            <ul tabindex="-1" class="menu dropdown-content bg-sub rounded-box z-1 mt-3 p-2 shadow">
                <li class="text-base!"><a href="#home">Home</a></li>
                <li class="text-base!"><a href="#about">About Us</a></li>
                <li class="text-base!"><a href="#services">Our Services</a></li>
                <li class="text-base!"><a href="#contact">Contact Us</a></li>
            </ul>
        </div>
        <div class="flex">
            <div class="w-18 h-18 overflow-hidden mr-2 lg:mx-4 ">
                <img src={VetLogo} alt="Clinic Logo" class="w-full h-full">
            </div>
            <div class="flex flex-col justify-center">
                <h3 class="text-xl lg:text-2xl ">Dr. Rosario Vet Clinic</h3>
                <p class="text-xs lg:text-xs">237 A Malhacan Rd., Meycauayan, Bulacan, Philippines</p>
            </div>
        </div>
    </div>
    <div class="navbar-end hidden lg:flex">
        <ul class="menu menu-horizontal px-1">
            <li><a class="text-base!"href="#home">Home</a></li>
            <li><a class="text-base!"href="#about">About Us</a></li>
            <li><a class="text-base!"href="#services">Our Services</a></li>
            <li><a class="text-base!"href="#contact">Contact Us</a></li>
        </ul>
    </div>
</div>