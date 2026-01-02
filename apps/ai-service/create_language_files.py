"""
언어별 HTML 파일 생성 스크립트
기본 index.html을 기반으로 언어별로 번역된 버전을 생성합니다.
"""

import re

# 언어별 번역 데이터
translations = {
    'ko': {
        'title': 'Uvolution AI | 예측 아이트래킹',
        'description': 'DeepGaze IIE를 사용하여 96% 정확도로 사용자 주의를 예측합니다.',
        'nav_features': '기능',
        'nav_reports': '보고서',
        'nav_science': '과학',
        'nav_pricing': '가격',
        'nav_home': '홈',
        'try_it_now': '지금 사용해보기',
        'heading': 'Uvolution AI',
        'tagline': '96% 정확도로 사용자 주의 예측',
        'info': 'DeepGaze IIE &#38; MIT1003 데이터셋 기반',
        'analyze_design': '디자인 분석하기',
        'analyze_desc': 'UI 디자인을 업로드하여 즉시 예측 히트맵을 생성하세요.',
        'comprehensive_reports': '종합 분석 보고서',
        'comprehensive_desc': '인지 과학 및 A/B 테스트 연구를 기반으로 한 실용적인 인사이트',
        'predictive_heatmaps': '예측 히트맵',
        'predictive_desc': '사용자가 먼저 볼 위치를 정확히 확인하세요. 최대 주의를 위해 레이아웃을 최적화하세요.',
        'color_psychology': '색상 심리학',
        'color_desc': '전환율을 최대 34% 향상시키는 것으로 입증된 CTA 색상 추천을 받아보세요.',
        'ux_recommendations': 'UX 추천',
        'ux_desc': '여백 분석, 시각적 계층 구조, CTA 배치, 모바일 친화성 등.',
        'try_now_free': '지금 무료로 사용해보기',
        'trusted': '디자이너들의 신뢰',
        'testimonial_1': '"놀라운 정확도. UI 디자인 접근 방식을 바꿨습니다."',
        'testimonial_2': '"모든 UX 연구자에게 필수 도구입니다."',
        'testimonial_3': '"수주의 테스트 시간을 절약했습니다."',
        'navigation': '네비게이션',
        'contact': '연락처',
        'footer_desc': '현대 웹을 위한 예측 아이트래킹.&#60;br&#62;딥러닝 기반.',
        'login': '로그인',
        'signup': '가입',
        'email_address': '이메일 주소',
        'password': '비밀번호',
        'name': '이름',
        'or_login_with': '또는 다음으로 로그인',
        'or_signup_with': '또는 다음으로 가입',
        'create_account': '계정 만들기',
    },
    'en': {
        'selected': 'en',
        # English is default, no translations needed
    },
    'cn': {
        'title': 'Uvolution AI | 预测眼球追踪',
        'description': '使用DeepGaze IIE以96%的准确度预测用户注意力。',
        'nav_features': '功能',
        'nav_reports': '报告',
        'nav_science': '科学',
        'nav_pricing': '定价',
        'nav_home': '首页',
        'try_it_now': '立即试用',
        'heading': 'Uvolution AI',
        'tagline': '96%准确度预测用户注意力',
        'info': '基于DeepGaze IIE &#38; MIT1003数据集',
        'analyze_design': '分析您的设计',
        'analyze_desc': '上传UI设计以立即生成预测热图。',
        'comprehensive_reports': '综合分析报告',
        'comprehensive_desc': '获得基于认知科学和A/B测试研究的可操作见解',
        'predictive_heatmaps': '预测热图',
        'predictive_desc': '准确查看用户首先会看到的位置。优化您的布局以获得最大注意力。',
        'color_psychology': '色彩心理学',
        'color_desc': '获取经证实可将转化率提高34%的CTA颜色建议。',
        'ux_recommendations': 'UX建议',
        'ux_desc': '空白分析、视觉层次、CTA放置、移动友好性等。',
        'try_now_free': '免费试用',
        'trusted': '设计师信赖',
        'testimonial_1': '"令人难以置信的准确性。它改变了我们的UI设计方法。"',
        'testimonial_2': '"任何UX研究人员的必备工具。"',
        'testimonial_3': '"为我们节省了数周的测试时间。"',
        'navigation': '导航',
        'contact': '联系方式',
        'footer_desc': '现代网络的预测眼球追踪。&#60;br&#62;由深度学习提供支持。',
        'login': '登录',
        'signup': '注册',
        'email_address': '电子邮件地址',
        'password': '密码',
        'name': '姓名',
        'or_login_with': '或使用以下方式登录',
        'or_signup_with': '或使用以下方式注册',
        'create_account': '创建账户',
    },
    'jp': {
        'title': 'Uvolution AI | 予測的アイトラッキング',
        'description': 'DeepGaze IIEを使用して96%の精度でユーザーの注意を予測します。',
        'nav_features': '機能',
        'nav_reports': 'レポート',
        'nav_science': '科学',
        'nav_pricing': '価格',
        'nav_home': 'ホーム',
        'try_it_now': '今すぐ試す',
        'heading': 'Uvolution AI',
        'tagline': '96%の精度でユーザーの注意を予測',
        'info': 'DeepGaze IIE &#38; MIT1003データセットを使用',
        'analyze_design': 'デザインを分析',
        'analyze_desc': 'UIデザインをアップロードして、すぐに予測ヒートマップを生成します。',
        'comprehensive_reports': '包括的な分析レポート',
        'comprehensive_desc': '認知科学とA/Bテスト研究に裏付けられた実用的なインサイトを取得',
        'predictive_heatmaps': '予測ヒートマップ',
        'predictive_desc': 'ユーザーが最初に見る場所を正確に確認できます。最大限の注意を引くためにレイアウトを最適化します。',
        'color_psychology': '色彩心理学',
        'color_desc': 'コンバージョン率を最大34%向上させることが証明されたCTA色の推奨を取得します。',
        'ux_recommendations': 'UX推奨事項',
        'ux_desc': '余白分析、視覚的階層、CTA配置、モバイルフレンドリー性など。',
        'try_now_free': '今すぐ無料で試す',
        'trusted': 'デザイナーに信頼されています',
        'testimonial_1': '"信じられない精度。UIデザインへのアプローチが変わりました。"',
        'testimonial_2': '"すべてのUX研究者にとって必須のツールです。"',
        'testimonial_3': '"数週間のテスト時間を節約しました。"',
        'navigation': 'ナビゲーション',
        'contact': 'お問い合わせ',
        'footer_desc': '現代のウェブのための予測的アイトラッキング。&#60;br&#62;ディープラーニングを使用。',
        'login': 'ログイン',
        'signup': '登録',
        'email_address': 'メールアドレス',
        'password': 'パスワード',
        'name': '名前',
        'or_login_with': 'または以下でログイン',
        'or_signup_with': 'または以下で登録',
        'create_account': 'アカウント作成',
    }
}

def create_lang_file(lang_code):
    """언어별 HTML 파일 생성"""
    
    # 기본 파일 읽기
    with open('static/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if lang_code == 'en':
        # 영어는 기본값이므로 선택만 변경
        content = content.replace(
            '<option value="ko">한국어</option>',
            f'<option value="ko">한국어</option>'
        )
        content = content.replace(
            '<option value="en">English</option>',
            f'<option value="en" selected>English</option>'
        )
    elif lang_code in translations:
        trans = translations[lang_code]
        
        # 선택된 언어 설정
        content = content.replace(
            f'<option value="{lang_code}">',
            f'<option value="{lang_code}" selected>'
        )
        
        # 타이틀 및 메타 설명
        if 'title' in trans:
            content = re.sub(
                r'<title>.*?</title>',
                f'<title>{trans["title"]}</title>',
                content
            )
        if 'description' in trans:
            content = re.sub(
                r'<meta name="description" content=".*?"',
                f'<meta name="description" content="{trans["description"]}"',
                content
            )
        
        # 네비게이션
        if 'nav_home' in trans:
            content = content.replace('>Home</a>', f'>{trans["nav_home"]}</a>')
        if 'nav_features' in trans:
            content = content.replace('>Features</a>', f'>{trans["nav_features"]}</a>')
        if 'nav_reports' in trans:
            content = content.replace('>Reports</a>', f'>{trans["nav_reports"]}</a>')
        if 'nav_science' in trans:
            content = content.replace('>Science</a>', f'>{trans["nav_science"]}</a>')
        if 'nav_pricing' in trans:
            content = content.replace('>Pricing</a>', f'>{trans["nav_pricing"]}</a>')
        if 'try_it_now' in trans:
            content = content.replace('>Try It Now</a>', f'>{trans["try_it_now"]}</a>')
        
        # 히어로 섹션
        if 'tagline' in trans:
            content = content.replace('>Predict User Attention with 96% Accuracy</p>', f'>{trans["tagline"]}</p>')
        if 'info' in trans:
            content = content.replace('>Powered by DeepGaze IIE &amp; MIT1003 Dataset</span>', f'>{trans["info"]}</span>')
        
        # 위젯 섹션
        if 'analyze_design' in trans:
            content = content.replace('>Analyze Your Design</h2>', f'>{trans["analyze_design"]}</h2>')
        if 'analyze_desc' in trans:
            content = content.replace('>Upload a UI design to generate a predictive heatmap instantly.</p>', f'>{trans["analyze_desc"]}</p>')
        
        # 보고서 섹션
        if 'comprehensive_reports' in trans:
            content = content.replace('>Comprehensive Analysis Reports', f'>{trans["comprehensive_reports"]}')
        if 'comprehensive_desc' in trans:
            content = content.replace('>Get actionable insights backed by cognitive science', f'>{trans["comprehensive_desc"]}')
        if 'predictive_heatmaps' in trans:
            content = content.replace('>Predictive Heatmaps</h3>', f'>{trans["predictive_heatmaps"]}</h3>')
        if 'predictive_desc' in trans:
            content = content.replace('>See exactly where users will look', f'>{trans["predictive_desc"]}')
        if 'color_psychology' in trans:
            content = content.replace('>Color Psychology</h3>', f'>{trans["color_psychology"]}</h3>')
        if 'color_desc' in trans:
            content = content.replace('>Get CTA color recommendations', f'>{trans["color_desc"]}')
        if 'ux_recommendations' in trans:
            content = content.replace('>UX Recommendations</h3>', f'>{trans["ux_recommendations"]}</h3>')
        if 'ux_desc' in trans:
            content = content.replace('>Whitespace analysis, visual', f'>{trans["ux_desc"]}')
        if 'try_now_free' in trans:
            content = content.replace('>Try It Now - Free</a>', f'>{trans["try_now_free"]}</a>')
        
        # Testimonials
        if 'trusted' in trans:
            content = content.replace('>Trusted by Designers</h2>', f'>{trans["trusted"]}</h2>')
        
        # Footer
        if 'navigation' in trans:
            content = content.replace('>Navigation</h4>', f'>{trans["navigation"]}</h4>')
        if 'contact' in trans:
            content = content.replace('>Contact</h4>', f'>{trans["contact"]}</h4>')
        if 'footer_desc' in trans:
            content = content.replace('>Predictive eye tracking for the modern web.<br>Powered by Deep Learning.</p>', f'>{trans["footer_desc"]}</p>')
        
        # Login/Signup modals
        if 'login' in trans:
            content = content.replace('id="loginModalLabel">Login</h4>', f'id="loginModalLabel">{trans["login"]}</h4>')
        if 'signup' in trans:
            content = content.replace('id="signupModalLabel">Sign Up</h4>', f'id="signupModalLabel">{trans["signup"]}</h4>')
        if 'email_address' in trans:
            content = content.replace('for="loginEmail">Email address</label>', f'for="loginEmail">{trans["email_address"]}</label>')
            content = content.replace('for="signupEmail">Email address</label>', f'for="signupEmail">{trans["email_address"]}</label>')
        if 'password' in trans:
            content = content.replace('for="loginPassword">Password</label>', f'for="loginPassword">{trans["password"]}</label>')
            content = content.replace('for="signupPassword">Password</label>', f'for="signupPassword">{trans["password"]}</label>')
        if 'name' in trans:
            content = content.replace('for="signupName">Name</label>', f'for="signupName">{trans["name"]}</label>')
        if 'login' in trans:
            content = content.replace('type="submit" class="btn btn-primary btn-block">Login</button>', f'type="submit" class="btn btn-primary btn-block">{trans["login"]}</button>')
        if 'create_account' in trans:
            content = content.replace('type="submit" class="btn btn-primary btn-block">Create Account</button>', f'type="submit" class="btn btn-primary btn-block">{trans["create_account"]}</button>')
    
    # 파일 저장
    output_file = f'static/index_{lang_code}.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Created: {output_file}')

# 모든 언어 파일 생성
for lang in ['ko', 'en', 'cn', 'jp']:
    create_lang_file(lang)

print('\n모든 언어 파일 생성 완료!')
