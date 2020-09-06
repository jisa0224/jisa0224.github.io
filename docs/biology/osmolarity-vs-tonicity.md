# 滲透性（Osmolarity）vs. 張性（Tonicity），及滲透濃度（Osmolarity）

## 滲透性（Osmolarity）vs. 張性（Tonicity）

> Osmolarity and tonicity are related but distinct concepts. Thus, the terms ending in -osmotic (isosmotic, hyperosmotic, hyposmotic) are not synonymous with the terms ending in -tonic (isotonic, hypertonic, hypotonic). The terms are related in that they **both compare the solute concentrations of two solutions separated by a membrane**. The terms are different because **osmolarity takes into account the total concentration of penetrating solutes and non-penetrating solutes**, whereas **tonicity takes into account the total concentration of non-freely penetrating solutes only**.
> 
> Penetrating solutes can diffuse through the cell membrane, causing momentary changes in cell volume as the solutes "pull" water molecules with them. Non-penetrating solutes cannot cross the cell membrane; therefore, the movement of water across the cell membrane (i.e., osmosis) must occur for the solutions to reach equilibrium.
> 
> A solution can be both hyperosmotic and isotonic. For example, the intracellular fluid and extracellular can be hyperosmotic, but isotonic – if the total concentration of solutes in one compartment is different from that of the other, but one of the ions can cross the membrane (in other words, a penetrating solute), drawing water with it, thus causing no net change in solution volume.
> 
> [Osmotic concentration - Wikipedia](https://en.wikipedia.org/wiki/Osmotic_concentration#Osmolarity_vs._tonicity)

滲透性和張性討論的都是被膜分開的兩溶液的濃度，但是

- 滲透性：不可通過膜的溶質 + 可通過膜的溶質
- 張性：不可通過膜的溶質

只考慮單一溶質時

- 不可通過膜的溶質，**水**由**低張往高張**溶液移動以達成平衡
- 可同過膜的溶質，**溶質**由**高滲透壓溶液往低滲透壓**溶液移動以達成平衡

所以「等張但高滲透壓」的溶液是存在的，例如：在血漿中的紅血球，兩者必須等張，不然紅血球會膨脹或萎縮，但單看 Na<sup>+</sup> 離子時，血漿是高滲透壓的，因為血漿的 Na<sup>+</sup> 濃度高於紅血球內，在這種情況下，膜兩側沒有水（溶劑）的淨移動，但 Na<sup>+</sup> 可以移動。

## 滲透濃度（Osmolarity）

滲透濃度（Osmotic concentration 或 Osmolarity）是表示溶液內所有溶質的濃度，與一般的濃度相比，需要考慮電解質解離的情況。

<table>
    <tbody>
        <tr>
            <th width="5%">&nbsp;</th>
            <th width="45%" style="text-align: center;">體積莫爾濃度<br />Molarity</th>
            <th width="45%" style="text-align: center;">體積滲透濃度<br />Osmolarity</th>
        </tr>
        <tr>
            <td style="text-align: center; vertical-align: middle">單位</td>
            <td style="text-align: center; vertical-align: middle">M 或 mol/L</td>
            <td style="text-align: center; vertical-align: middle">Osm/L</td>
        </tr>
        <tr>
            <td style="text-align: center; vertical-align: middle">定義</td>
            <td style="text-align: center; vertical-align: middle">$$c=\frac{n}{V}=\frac{\frac{N}{N_A}}{V}$$</td>
            <td style="text-align: center; vertical-align: middle">$$\text{osmolarity}=\frac{\text{osmole}}{V}=\frac{\sum_i \varphi_i n_i c_i}{V}=\frac{\sum_i i_i c_i}{V}$$</td>
        </tr>
        <tr>
            <td style="text-align: center; vertical-align: middle">參數</td>
            <td>
                <ul>
                    <li>$V$ 為體積</li>
                    <li>$n$ 為溶質莫爾數</li>
                    <li>$N$ 為溶質分子數</li>
                    <li>$N_A$ 為亞佛加厥常數</li>
                </ul>
            </td>
            <td>
                <ul>
                    <li>下標 $i$ 為溶質總類</li>
                    <li>$\varphi$ 為溶質的&nbsp;osmotic coefficient，表示解離的程度，非電解質為 0，理想電解質為 1</li>
                    <li>$n$ 為離子總數（eg: 葡萄糖為 1，NaCl 為 2，MgCl<sub>2</sub> 為 3）</li>
                    <li>$c$ 為溶質的體積莫爾濃度</li>
                    <li>$i$ 為溶值的&nbsp;van 't Hoff factor，$i=\varphi n$</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td style="text-align: center; vertical-align: middle">對象</td>
            <td style="text-align: center; vertical-align: middle">單一溶質</td>
            <td style="text-align: center; vertical-align: middle">所有溶質</td>
        </tr>
        <tr>
            <td style="text-align: center; vertical-align: middle">說明</td>
            <td>&nbsp;</td>
            <td>對相同體積莫爾濃度的葡萄糖溶液和 NaCl 溶液，其體積滲透濃度不同，後者會是前者的大約 2 倍&nbsp;</td>
        </tr>
    </tbody>
</table>

滲透濃度可以用來計算出滲透壓（Osmotic pressure）。

## 參考資料

[Osmotic concentration - Wikipedia](https://en.wikipedia.org/wiki/Osmotic_concentration)
 
