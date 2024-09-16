
<template>
    <div class="container-fluid">
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="#">SkillLink</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="true" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" font-weight="bold" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#">Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Sign Up</a>
                    </li>
                </ul>
            </div>
        </nav>

        <!--Welcome Section-->
        <div class="welcome-section">
            <div class="section-box">
                <h1>Welcome to SkillLink</h1>
                <p class="lead">Search through thousands of job opportunities or skilled professionals near you.</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'LandingPage',
};
</script>

<style scoped>
.welcome-section {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;
    height: 100vh;
    background: linear-gradient(to top, #013220, rgba(1, 50, 32, 0.1));
    color: white;
}
.section-box {
    background-color: #f1f1f1;
    padding: 60px;
    border-radius: 30px;
    box-shadow: 0px, 4px, 10px rgba(0, 0, 0, 0.1);
    text-align: center;
}
.section-box h1 {
    font-size: 3rem;
    color: #008080;
    font-weight: bold;
}
.navbar-brand {
    font-weight: bold;
}
.section-box p.lead {
    font-size: 1.25rem;
    margin-top: 20px;
    color: #6c757d;
}

@media (max-width: 768px) {
    .navbar-brand {
        font-size: 1.25rem;
    }
    .section-box {
        padding: 30px;
    }
    .section-box h1 {
        font-size: 2.5rem;
    }
    .section-box p.lead {
        font-size: 1.1rem;
    }
}
</style>