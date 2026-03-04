<script lang="ts">
import VetLogo from "$lib/assets/VetLogo.png"
</script>
<div class="footer sm:footer-horizontal bg-main text-base-content p-10">
  <aside>
  <div class="w-20 h-20 overflow-hidden object-cover shrink-0">
    <img src={VetLogo} alt="Company Logo" class="w-full h-full">
  </div>
    <p>
    Dr. Rosario Veterinary Clinic
      <br />
    Providing reliable veterinary care since 1998
    </p>
  </aside>
  <nav>
    <h6 class="footer-title">Company</h6>
    <a href="#about" class="link link-hover">About us</a>
    <a href="#contact" class="link link-hover">Contact</a>
    <a href="#book" class="link link-hover">Book Now</a>
  </nav>
  <nav>
    <h6 class="footer-title">Legal</h6>
    <a href="/terms-and-condition" class="link link-hover">Terms of use</a>
    <a href="/privacy-and-policy" class="link link-hover">Privacy policy</a>
    <a href="/cookies" class="link link-hover">Cookie policy</a>
  </nav>
</div>

