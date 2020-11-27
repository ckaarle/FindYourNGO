package com.example.findyourngo

import android.os.Bundle
import android.view.MenuItem
import com.google.android.material.bottomnavigation.BottomNavigationView
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import com.example.findyourngo.ui.favourites.FavouritesFragment
import com.example.findyourngo.ui.maps.MapsFragment
import com.example.findyourngo.ui.overview.OverviewFragment
import com.google.android.material.navigation.NavigationView

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val navView: BottomNavigationView = findViewById(R.id.nav_view)
        navView.setOnNavigationItemSelectedListener(navigationItemSelectedListener)

        if (savedInstanceState == null) {
            val fragment = MapsFragment()
            supportFragmentManager
                    .beginTransaction()
                    .replace(R.id.container, fragment, fragment.javaClass.getSimpleName())
                    .commit()
        }
    }

    private val navigationItemSelectedListener = BottomNavigationView.OnNavigationItemSelectedListener { menuItem ->
        when (menuItem.itemId) {
            R.id.navigation_maps -> {
                val fragment = MapsFragment()
                supportFragmentManager.beginTransaction().replace(R.id.container, fragment, fragment.javaClass.getSimpleName())
                        .commit()
                return@OnNavigationItemSelectedListener true
            }
            R.id.navigation_overview -> {
                val fragment = OverviewFragment()
                supportFragmentManager.beginTransaction().replace(R.id.container, fragment, fragment.javaClass.getSimpleName())
                        .commit()
                return@OnNavigationItemSelectedListener true
            }
            R.id.navigation_favourites -> {
                val fragment = FavouritesFragment()
                supportFragmentManager.beginTransaction().replace(R.id.container, fragment, fragment.javaClass.getSimpleName())
                        .commit()
                return@OnNavigationItemSelectedListener true
            }
        }
        false
    }
}