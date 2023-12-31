import React, { useState } from 'react'
import '../css/LanguageToggle.css'


/**
 * 
 * @returns 언어 선택 토글
 */
const LanguageToggle = (props) => {
    //언어 데이터
    let [langData, setlangData] = useState([
        { code: 'ko', tooltip: 'ko', flow: 'down', flag: 'south-korea' },
        { code: 'en', tooltip: 'en', flow: 'down', flag: 'united-kingdom' },
        { code: 'ja', tooltip: 'ja', flow: 'down', flag: 'japan' },
        { code: 'vi', tooltip: 'vi', flow: 'down', flag: 'vietnam' },
        { code: 'zh-CN', tooltip: 'zh-CN', flow: 'up', flag: 'china' }
    ]);

    const [selectedLang, setSelectedLang] = useState(langData[0]); //선택된 언어

    //언어 선택 시 호출
    const handleLangSelect = (lang) => {
        setSelectedLang(lang);
        props.languageSelection(lang)
        const selectedLanguageIndex = langData.findIndex((element) => element.code ===lang.code)
        langData[selectedLanguageIndex]=langData[0]
        langData[0]=lang
        // 순서 변경
        for(let i=0; i<langData.length;i++)
        {
            langData[i].flow='down'
            if(langData.length-1===i){
                langData[i].flow='up'
            }
        }
        setlangData(langData) //언어 적용
    };

    return (
        <div id="select-container">
            <ul>
                {langData.map((lang) => (
                    <li
                        key={lang.code}
                        lang-selection={lang.code}
                        tooltip={lang.tooltip}
                        flow={lang.flow}
                        onClick={() => handleLangSelect(lang)}
                        className={selectedLang.code === lang.code ? 'selected' : ''}
                    >
                        <img
                            src={`https://cdn.countryflags.com/thumbs/${lang.flag}/flag-800.png`}
                            alt={lang.code}
                            className="flag-img"
                        />
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default LanguageToggle
