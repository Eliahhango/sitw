$root = 'c:\Users\hango\Desktop\Site downloader\downloaded_site\profilez.xyz'
$files = Get-ChildItem -Path $root -Recurse -Filter *.html

$inject = @"
<style id="elitechwiz-white-theme">
:root { --color-primary: #0B0840; }
body, body.light-version { background: #ffffff !important; color: #1f2937 !important; }
.template-header, .template-footer, .hero-area, .skill-section, .counter-section,
.section-gap, .section-gap-bottom, .contact-section, .page-content-section,
.single-service-box, .single-latest-post, .testimonial-box, .project-item,
.footer-content, .footer-copyright, .breadcrumbs-section {
    background: #ffffff !important;
    color: #1f2937 !important;
}
.navbar .nav-link, .navbar-brand, h1, h2, h3, h4, h5, h6, p, li, span, label, a {
    color: #1f2937 !important;
}
.main-btn, .filled-btn, .go-home-btn { background: #0B0840 !important; color: #ffffff !important; border-color: #0B0840 !important; }
.template-footer .overlay, .overlay { display: none !important; }
</style>
"@

foreach ($f in $files) {
    $c = Get-Content -Raw -LiteralPath $f.FullName

    $c = $c -replace '(?i)Profilex', 'EliTechWiz'
    $c = $c -replace '(?i)ronaldcortez', 'elitechwiz'

    $c = $c -replace 'href="/user/login/"', 'href="/elitechwiz/user/login/"'
    $c = $c -replace 'href="https://profilez\.xyz/elitechwiz/user/login"', 'href="/elitechwiz/user/login/"'
    $c = $c -replace 'href="https://profilez\.xyz/login"', 'href="/elitechwiz/user/login/"'
    $c = $c -replace 'href="/login"', 'href="/elitechwiz/user/login/"'

    $c = $c -replace 'class="dark-version"', 'class="light-version"'
    $c = $c -replace 'navbar-dark', 'navbar-light'
    $c = $c -replace 'bg-primary-color', 'bg-white'

    $c = $c -replace 'https://profilez\.xyz/elitechwiz', '/elitechwiz'
    $c = $c -replace '//profilez\.xyz/', '/'
    $c = $c -replace 'https://profilez\.xyz/', '/'
    $c = $c -replace 'https://profilez\.xyz', ''

    if ($c -notmatch 'elitechwiz-white-theme') {
        $c = $c -replace '</head>', ($inject + "`r`n</head>")
    }

    Set-Content -LiteralPath $f.FullName -Value $c -Encoding UTF8
}

Write-Host "Updated $($files.Count) HTML files."
