/**
 * Script pour télécharger les polices Google Fonts
 * Usage: node scripts/download-fonts.js
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const FONTS_DIR = path.join(__dirname, '..', 'assets', 'fonts');

// Créer le dossier fonts s'il n'existe pas
if (!fs.existsSync(FONTS_DIR)) {
  fs.mkdirSync(FONTS_DIR, { recursive: true });
}

const fonts = [
  {
    name: 'Open Sans',
    files: [
      { url: 'https://github.com/google/fonts/raw/main/apache/opensans/OpenSans%5Bwdth%2Cwght%5D.ttf', output: 'OpenSans-Regular.ttf' },
    ]
  },
  {
    name: 'Josefin Sans',
    files: [
      { url: 'https://github.com/google/fonts/raw/main/ofl/josefinsans/JosefinSans%5Bwght%5D.ttf', output: 'JosefinSans-Regular.ttf' },
    ]
  },
  {
    name: 'Anton',
    files: [
      { url: 'https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf', output: 'Anton-Regular.ttf' },
    ]
  },
  {
    name: 'Antonio',
    files: [
      { url: 'https://github.com/google/fonts/raw/main/ofl/antonio/Antonio%5Bwght%5D.ttf', output: 'Antonio-Regular.ttf' },
    ]
  },
  {
    name: 'Bangers',
    files: [
      { url: 'https://github.com/google/fonts/raw/main/ofl/bangers/Bangers-Regular.ttf', output: 'Bangers-Regular.ttf' },
    ]
  },
  {
    name: 'Cookie',
    files: [
      { url: 'https://github.com/google/fonts/raw/main/ofl/cookie/Cookie-Regular.ttf', output: 'Cookie-Regular.ttf' },
    ]
  },
  {
    name: 'Allan',
    files: [
      { url: 'https://github.com/google/fonts/raw/main/ofl/allan/Allan-Regular.ttf', output: 'Allan-Regular.ttf' },
    ]
  },
  {
    name: 'Luckiest Guy',
    files: [
      { url: 'https://github.com/google/fonts/raw/main/ofl/luckiestguy/LuckiestGuy-Regular.ttf', output: 'LuckiestGuy-Regular.ttf' },
    ]
  },
  {
    name: 'Ubuntu',
    files: [
      { url: 'https://github.com/google/fonts/raw/main/ufl/ubuntu/Ubuntu-Regular.ttf', output: 'Ubuntu-Regular.ttf' },
    ]
  },
];

console.log('📥 Téléchargement des polices Google Fonts...\n');

function downloadFont(url, outputPath, fontName) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(outputPath);
    
    https.get(url, (response) => {
      if (response.statusCode === 302 || response.statusCode === 301) {
        // Suivre la redirection
        https.get(response.headers.location, (redirectResponse) => {
          redirectResponse.pipe(file);
          file.on('finish', () => {
            file.close();
            console.log(`✅ ${fontName} téléchargée`);
            resolve();
          });
        }).on('error', reject);
      } else {
        response.pipe(file);
        file.on('finish', () => {
          file.close();
          console.log(`✅ ${fontName} téléchargée`);
          resolve();
        });
      }
    }).on('error', (err) => {
      fs.unlink(outputPath, () => {});
      reject(err);
    });
  });
}

async function downloadAllFonts() {
  for (const font of fonts) {
    for (const file of font.files) {
      const outputPath = path.join(FONTS_DIR, file.output);
      
      // Vérifier si le fichier existe déjà
      if (fs.existsSync(outputPath)) {
        console.log(`⏭️  ${file.output} existe déjà, ignoré`);
        continue;
      }
      
      try {
        await downloadFont(file.url, outputPath, file.output);
      } catch (error) {
        console.error(`❌ Erreur lors du téléchargement de ${file.output}:`, error.message);
        console.log(`   Téléchargez manuellement depuis: ${file.url}`);
      }
    }
  }
  
  console.log('\n✨ Téléchargement terminé!');
  console.log(`📁 Les polices sont dans: ${FONTS_DIR}`);
  console.log('\n💡 Note: Certaines polices peuvent nécessiter un téléchargement manuel depuis Google Fonts.');
  console.log('   Consultez assets/fonts/README.md pour plus d\'informations.');
}

downloadAllFonts().catch(console.error);
